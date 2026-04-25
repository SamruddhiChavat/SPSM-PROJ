import streamlit as st
from services import chat_service

def render():
    st.markdown("""
        <h2 style='color: #ffffff; font-family: "Inter", sans-serif; margin-bottom: 0px;'>🌐 Global Security Chat</h2>
        <p style='color: #8e918f; font-size: 14px; margin-bottom: 20px;'>A shared channel for all platform users to communicate in real-time.</p>
    """, unsafe_allow_html=True)

    current_user = st.session_state.get("user", "Anonymous")

    # --- CHAT DISPLAY AREA ---
    # We wrap this in a container to manage the height
    chat_container = st.container(height=500, border=True)
    
    with chat_container:
        messages = chat_service.get_chat_history()
        
        if not messages:
            st.info("No messages yet. Start the conversation!")
        
        for msg in messages:
            # Determine if the message is from the current user or someone else
            is_me = msg['sender'] == current_user
            with st.chat_message("user" if is_me else "assistant"):
                st.write(f"**{msg['sender']}**")
                st.write(msg['text'])

    # --- CHAT INPUT ---
    if prompt := st.chat_input("Type your message here..."):
        # Send to Firebase
        chat_service.send_message(current_user, prompt)
        # Rerun to update the message list immediately
        st.rerun()