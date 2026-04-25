import streamlit as st
import datetime
from services import auth_service, email_service, activity_service
from utils.firebase_init import get_db

def render():
    # --- CSS STYLING ---
    st.markdown("""
        <style>
        [data-testid="stVerticalBlock"] > div:nth-child(3) [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: rgba(255, 75, 75, 0.05);
            border: 1px solid #ff4b4b !important;
            border-radius: 12px;
        }
        [data-testid="stVerticalBlock"] > div:nth-child(5) [data-testid="stVerticalBlockBorderWrapper"] {
            background-color: rgba(91, 179, 119, 0.05);
            border: 1px solid #5bb377 !important;
            border-radius: 12px;
        }
        .stButton > button[kind="primary"] {
            background-color: #ff4b4b;
            color: white;
            font-weight: bold;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("## 🚨 Incident Response & Recovery")
    
    current_user = st.session_state.get("user")
    db = get_db()
    
    if not current_user:
        st.error("Please log in to access the Secure Portal.")
        return

    # --- SECTION 1: EMERGENCY LOCKDOWN (Incident Response) ---
    with st.container(border=True):
        st.subheader("🛑 EMERGENCY LOCKDOWN")
        if st.button("EXECUTE GLOBAL LOCKDOWN", type="primary", use_container_width=True):
            db.collection("users").document(current_user).update({"account_status": "locked"})
            activity_service.log_activity(current_user, "CRITICAL: Global Lockdown Triggered")
            st.warning("Account Locked. Use the remediation workflow below to restore access.")

    st.write("")

    # --- SECTION 2: EMAIL-BASED REMEDIATION ---
    with st.container(border=True):
        st.subheader("🛡️ EMAIL REMEDIATION")
        
        if "recovery_status" not in st.session_state:
            st.session_state["recovery_status"] = "send_email"

        # PHASE 1: SENDING THE CODE
        if st.session_state["recovery_status"] == "send_email":
            target_email = st.text_input("Enter Recovery Email Address", placeholder="user@example.com")
            
            if st.button("Send Verification Code", use_container_width=True):
                if target_email:
                    with st.spinner("Sending..."):
                        success, result = email_service.send_recovery_email(target_email)
                        if success:
                            st.session_state["sent_token"] = result
                            st.toast(f"Code sent to {target_email}!", icon="📧")
                        else:
                            st.error(f"Error: {result}")
                else:
                    st.warning("Please enter an email address.")

            # PHASE 2: VALIDATING THE CODE
            token_input = st.text_input("Enter 6-Digit Code", placeholder="XXXXXX")
            if st.button("Validate Identity", use_container_width=True):
                if token_input == st.session_state.get("sent_token") and token_input:
                    st.session_state["recovery_status"] = "reset_password"
                    st.rerun()
                else:
                    st.error("Invalid token.")

        # PHASE 3: PASSWORD RESET
        elif st.session_state["recovery_status"] == "reset_password":
            st.success("✅ Identity Verified.")
            new_pass = st.text_input("New Password", type="password")
            conf_pass = st.text_input("Confirm New Password", type="password")
            
            if st.button("Finalize Remediation", use_container_width=True):
                if new_pass == conf_pass and len(new_pass) >= 8:
                    hashed = auth_service.hash_password(new_pass)
                    db.collection("users").document(current_user).update({
                        "password": hashed,
                        "account_status": "active"
                    })
                    st.balloons()
                    st.success("Account Restored.")
                    st.session_state["recovery_status"] = "send_email" # Reset flow
                else:
                    st.error("Passwords must match (min 8 characters).")