#login ui
import streamlit as st
from services import auth_service, otp_service, jwt_service, activity_service

def render():
    # Use columns to center the login box
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔐 Secure System Login")
        st.write("Welcome! Please authenticate to access the secure portal.")
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])

        with tab1:
            username = st.text_input("Username", key="log_user")
            password = st.text_input("Password", type="password", key="log_pass")
            totp_code = st.text_input("6-Digit Google Authenticator Code", key="log_totp")
            
            if st.button("Authenticate", use_container_width=True):
                user_data = auth_service.get_user(username)
                if user_data and auth_service.verify_password(password, user_data["password"]):
                    if otp_service.verify_totp(user_data["totp_secret"], totp_code):
                        # Set session state on success
                        st.session_state["user"] = username
                        jwt_res = jwt_service.generate_token(username)
                        st.session_state["jwt_token"] = jwt_res
                        
                        activity_service.log_activity(username, "Successful Login via 2FA")
                        st.success("Authentication Successful! Redirecting...")
                        st.rerun()
                    else:
                        activity_service.log_activity(username, "Failed Login (Invalid 2FA)")
                        st.error("Invalid Authenticator Code.")
                else:
                    activity_service.log_activity(username if username else "Unknown", "Failed Login (Invalid Credentials)")
                    st.error("Invalid Username or Password.")

        with tab2:
            st.info("Registration requires setting up Google Authenticator.")
            new_user = st.text_input("Choose Username", key="reg_user")
            new_pass = st.text_input("Choose Password", type="password", key="reg_pass")
            
            if st.button("1. Generate 2FA QR Code"):
                if auth_service.get_user(new_user):
                    st.error("Username already taken.")
                elif len(new_pass) < 6:
                    st.error("Password must be at least 6 characters.")
                else:
                    secret = otp_service.generate_totp_secret()
                    qr_bytes = otp_service.get_qr_code(secret, new_user)
                    st.session_state["temp_secret"] = secret
                    st.image(qr_bytes, caption="Scan this with Google Authenticator or Authy")
                    
            if "temp_secret" in st.session_state:
                verify_code = st.text_input("2. Enter the 6-digit code from your app to verify")
                if st.button("Complete Registration", use_container_width=True):
                    if otp_service.verify_totp(st.session_state["temp_secret"], verify_code):
                        hashed = auth_service.hash_password(new_pass)
                        auth_service.create_user(new_user, hashed, st.session_state["temp_secret"])
                        activity_service.log_activity(new_user, "Account Created")
                        st.success("Account securely created! You can now log in.")
                        del st.session_state["temp_secret"]
                    else:
                        st.error("Invalid verification code. Try again.")