#file scan virus total api ui 
import streamlit as st
from services import file_service

def render():
    st.subheader("🛡️ Real-Time Malware Scanner")
    uploaded_file = st.file_uploader("Upload a file for security inspection", type=["png", "jpg", "pdf"])

    if uploaded_file:
        is_valid, msg = file_service.validate_file(uploaded_file.name, uploaded_file.size)
        
        if not is_valid:
            st.error(msg)
        else:
            if st.button("Start Deep Security Scan"):
                file_bytes = uploaded_file.read()
                
                # Perform the real API scan
                is_clean, scan_msg = file_service.scan_with_virustotal(file_bytes)
                
                if is_clean:
                    st.success(f"✅ {scan_msg}")
                    # Now allow them to proceed with the app logic...
                else:
                    st.error(f"🚨 {scan_msg}")