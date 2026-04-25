import streamlit as st
from utils.firebase_init import get_db
from datetime import datetime, timezone
from services import activity_service

def render():
    db = get_db()
    current_user = st.session_state["user"]
    
    # Fetch User Data for the Profile Header
    user_doc = db.collection("users").document(current_user).get().to_dict()
    user_email = user_doc.get("email", "N/A")
    account_status = user_doc.get("account_status", "Active")
    
    # --- PROFILE HEADER ---
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Profile Picture Placeholder
        st.markdown(f"""
            <div style="display: flex; justify-content: center; align-items: center; 
            background-color: #262730; border-radius: 50%; width: 120px; height: 120px; 
            border: 2px solid #5bb377; font-size: 50px;">
                👤
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.title(f"{current_user.capitalize()}")
        st.caption(f"📧 {user_email} | 🛡️ Status: {account_status.upper()}")
        if st.button("Edit Profile", use_container_width=True):
            st.info("Profile editing coming soon!")

    st.write("") # Spacer

    # --- TABS INTERFACE ---
    tab1, tab2, tab3 = st.tabs(["📊 Activity Feed", "✍️ Create Post", "📂 Account Info"])

    # --- TAB 1: ACTIVITY FEED ---
    with tab1:
        st.subheader("Your Timeline")
        posts_ref = db.collection("posts").where("author", "==", current_user).stream()
        posts = [doc.to_dict() for doc in posts_ref]
        posts.sort(key=lambda x: x["timestamp"], reverse=True)

        if not posts:
            st.info("You haven't shared any secure updates yet.")
        else:
            for post in posts:
                with st.container(border=True):
                    st.markdown(f"**{post['author']}** • <small>{post['visibility']}</small>", unsafe_allow_html=True)
                    st.write(post["content"])
                    st.caption(f"🕒 {post['timestamp'].strftime('%b %d, %Y - %H:%M')}")

    # --- TAB 2: CREATE POST ---
    with tab2:
        with st.form("new_post_form", clear_on_submit=True):
            st.subheader("New Secure Post")
            post_content = st.text_area("What's on your mind?", placeholder="This message is stored securely in Firebase...")
            
            # Allow user to override default visibility per post
            visibility = st.selectbox("Who can see this?", ["Public", "Private"])
            submitted = st.form_submit_button("Publish Post", use_container_width=True)
            
            if submitted and post_content:
                db.collection("posts").add({
                    "author": current_user,
                    "content": post_content,
                    "visibility": visibility,
                    "timestamp": datetime.now(timezone.utc)
                })
                activity_service.log_activity(current_user, f"Created a {visibility} post")
                st.success("Post synchronized to secure ledger!")
                st.rerun()

    # --- TAB 3: ACCOUNT INFO ---
    with tab3:
        st.subheader("System Metadata")
        st.json({
            "Username": current_user,
            "Role": user_doc.get("role", "User"),
            "Account Created": user_doc.get("created_at", "N/A"),
            "MFA Enabled": "mfa_secret" in user_doc,
            "Storage Path": f"user_data/{current_user}/"
        })