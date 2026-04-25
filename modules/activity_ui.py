import streamlit as st
from utils.firebase_init import get_db
import pandas as pd

def render():
    st.header("📈 Security Activity ")
    st.write("Monitoring user actions and security events.")
    
    db = get_db()
    
    # Add a refresh button
    st.button("🔄 Refresh Logs")
    
    docs = db.collection("activity_logs").order_by("timestamp", direction="DESCENDING").limit(20).stream()
    
    logs = []
    for doc in docs:
        data = doc.to_dict()
        # Format the timestamp
        time_str = data['timestamp'].strftime('%Y-%m-%d %H:%M:%S') if 'timestamp' in data else 'Unknown'
        logs.append({
            "Timestamp": time_str,
            "User": data.get('username', 'Unknown'),
            "Action/Event": data.get('action', 'Unknown'),
            "IP Address": data.get('ip', 'Unknown')
        })
        
    if logs:
        # Display as a clean dataframe
        df = pd.DataFrame(logs)
        st.dataframe(df, use_container_width=True, hide_index=True)
    else:
        st.info("No security logs found.")