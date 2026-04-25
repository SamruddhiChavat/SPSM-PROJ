#file encrypt decrypt service ui

import streamlit as st
from services.encryption_service import generate_file_key, encrypt_file_data, decrypt_file_data

def render():
    st.header("🔐 True Secure File Encryption")
    st.write("Generate a unique, single-use key for every file. We do not store your keys.")
    st.markdown("---")

    if "enc_temp_data" not in st.session_state:
        st.session_state.enc_temp_data = None
        st.session_state.enc_temp_key = None
        st.session_state.enc_temp_name = None

    col1, col2 = st.columns(2)

    # ==========================================
    # LEFT COLUMN: ENCRYPTION
    # ==========================================
    with col1:
        st.subheader("🔒 Encrypt File")
        
        uploaded_file = st.file_uploader("Upload file to encrypt", type=["png", "jpg", "pdf", "txt", "csv"])

        if uploaded_file is not None:
            file_bytes = uploaded_file.read()
            st.success(f"Loaded: '{uploaded_file.name}'")
            
            if st.session_state.enc_temp_name != uploaded_file.name:
                st.session_state.enc_temp_data = None
                st.session_state.enc_temp_key = None
                st.session_state.enc_temp_name = uploaded_file.name

            if st.button("Encrypt & Generate Key", use_container_width=True):
                st.session_state.enc_temp_key = generate_file_key()
                st.session_state.enc_temp_data = encrypt_file_data(file_bytes, st.session_state.enc_temp_key)
                
            if st.session_state.enc_temp_data is not None:
                st.warning("⚠️ Please download BOTH files below. You cannot decrypt without the key!")
                
                st.download_button(
                    label="🔑 Download Secret Key (.key)",
                    data=st.session_state.enc_temp_key,
                    file_name=f"{uploaded_file.name}.key",
                    mime="application/octet-stream",
                    use_container_width=True
                )
                
                st.download_button(
                    label="📦 Download Encrypted File (.enc)",
                    data=st.session_state.enc_temp_data,
                    file_name=f"encrypted_{uploaded_file.name}.enc",
                    mime="application/octet-stream",
                    use_container_width=True
                )

    # ==========================================
    # RIGHT COLUMN: DECRYPTION
    # ==========================================
    with col2:
        st.subheader("🔓 Decrypt File")
        st.write("Provide both the `.enc` file and its matching `.key` file.")
        
        encrypted_file = st.file_uploader("1. Upload encrypted (.enc) file", type=["enc"])
        key_file = st.file_uploader("2. Upload the matching secret (.key) file", type=["key", "txt"])
        
        if encrypted_file is not None and key_file is not None:
            enc_bytes = encrypted_file.read()
            raw_key_bytes = key_file.read()
            
            # --- THE BULLETPROOF KEY CLEANER ---
            # 1. Strip Mac/Windows UTF-8 invisible headers (BOM)
            if raw_key_bytes.startswith(b'\xef\xbb\xbf'):
                raw_key_bytes = raw_key_bytes[3:]
            
            # 2. Strip all spaces, newlines, and carriage returns
            clean_key = raw_key_bytes.replace(b'\r', b'').replace(b'\n', b'').replace(b' ', b'').strip()
            
            if st.button("Decrypt File", use_container_width=True):
                # Fernet keys MUST be exactly 44 bytes long. This tells us if the file was corrupted.
                if len(clean_key) != 44:
                    st.error(f"❌ Invalid Key Format! Expected 44 characters, but got {len(clean_key)}. Did you upload the correct file?")
                else:
                    try:
                        decrypted_data = decrypt_file_data(enc_bytes, clean_key)
                        original_name = encrypted_file.name.replace("encrypted_", "").replace(".enc", "")
                        
                        st.success("✅ File decrypted successfully! The key matches.")
                        st.download_button(
                            label="💾 Download Decrypted File",
                            data=decrypted_data,
                            file_name=f"decrypted_{original_name}",
                            mime="application/octet-stream",
                            use_container_width=True
                        )
                    except Exception:
                        st.error("❌ Decryption failed! The key length is correct, but it does NOT match this specific file.")