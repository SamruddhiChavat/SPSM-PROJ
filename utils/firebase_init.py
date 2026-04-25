import firebase_admin
from firebase_admin import credentials, firestore
from config import FIREBASE_CREDENTIALS_PATH
import streamlit as st

@st.cache_resource
def get_db():
    """
    Initializes the Firebase Admin SDK and returns the Firestore client.
    Uses @st.cache_resource to ensure the database connection is only 
    created once and shared across all Streamlit re-runs.
    """
    # Check if Firebase app is already initialized to prevent crash on rerun
    if not firebase_admin._apps:
        try:
            cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
        except FileNotFoundError:
            st.error(f"🚨 Firebase Credentials missing! Please ensure '{FIREBASE_CREDENTIALS_PATH}' is in the root folder.")
            st.stop()
        except Exception as e:
            st.error(f"🚨 Failed to initialize Firebase: {e}")
            st.stop()
            
    return firestore.client()