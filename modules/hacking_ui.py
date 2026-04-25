import streamlit as st
import time
# Important: The import name must match your filename exactly
from services import vulnerability_service

def render():
    st.markdown("""
        <h2 style='color: #ffffff; font-family: "Inter", sans-serif; margin-bottom: 0px;'>🛡️ Security Vulnerability Scanner</h2>
        <p style='color: #8e918f; font-size: 14px; margin-bottom: 30px;'>Audit local system configurations and network entry points.</p>
    """, unsafe_allow_html=True)

    # UI Action Trigger
    if st.button("INITIATE FULL SYSTEM SCAN", type="primary", use_container_width=True):
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Visual feedback for the scan progress
        scan_steps = [
            "Loading signatures...", 
            "Checking local network ports...", 
            "Auditing system file permissions...", 
            "Analyzing results..."
        ]
        
        for i, step in enumerate(scan_steps):
            status_text.markdown(f"🔍 `{step}`")
            progress_bar.progress((i + 1) * 25)
            time.sleep(0.6)

        # CORRECTED CALL: Using vulnerability_service instead of scanner_service
        results = vulnerability_service.run_system_audit()
        
        status_text.success("Scan Complete!")
        st.divider()

        # Dashboard Metrics
        m1, m2 = st.columns(2)
        with m1:
            color = "normal" if results["risk_level"] == "Low" else "inverse"
            st.metric("Detected Risk Level", results["risk_level"], delta_color=color)
        with m2:
            st.metric("Operating System", results["os_version"])

        # Display Vulnerabilities
        st.subheader("Vulnerability Findings")
        if not results["vulnerabilities"]:
            st.success("✅ Clean Scan: No common vulnerabilities detected in the current scope.")
        else:
            for vuln in results["vulnerabilities"]:
                st.markdown(f"""
                    <div style="background-color: rgba(255, 75, 75, 0.1); border-left: 5px solid #ff4b4b; padding: 15px; border-radius: 8px; margin-bottom: 12px;">
                        <span style="color: #ff4b4b; font-weight: bold; font-size: 12px;">CRITICAL FINDING</span>
                        <p style="color: white; margin: 5px 0 0 0; font-size: 14px;">{vuln}</p>
                    </div>
                """, unsafe_allow_html=True)

    # Additional Tooling for the Demo
    with st.expander("🛠️ Manual Reconnaissance Tools"):
        st.write("Check if a specific port is open on your localhost:")
        port_input = st.number_input("Target Port", min_value=1, max_value=65535, value=80)
        if st.button("Check Port Status"):
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            if s.connect_ex(("127.0.0.1", port_input)) == 0:
                st.error(f"Port {port_input} is OPEN (Potential Vulnerability)")
            else:
                st.success(f"Port {port_input} is CLOSED (Secure)")
            s.close()