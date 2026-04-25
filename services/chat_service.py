from utils.firebase_init import get_db
import datetime

def is_chat_authorized(username):
    """
    Checks the user's privacy setting in Firebase.
    If 'Private', they are blocked from global chat.
    """
    try:
        db = get_db()
        user_doc = db.collection("users").document(username).get()
        
        if user_doc.exists:
            privacy_status = user_doc.to_dict().get("default_visibility", "Public")
            # Logic: If Private, they are locked out of global communication
            if privacy_status == "Private":
                return False
        return True
    except Exception:
        return False

def send_message(sender, text):
    """Adds a message to the global Firebase collection."""
    db = get_db()
    message_data = {
        "sender": sender,
        "text": text,
        "timestamp": datetime.datetime.now()
    }
    db.collection("global_chat").add(message_data)

def get_chat_history(limit=50):
    """Fetches latest messages from the shared chatroom."""
    db = get_db()
    docs = db.collection("global_chat").order_by("timestamp", direction="DESCENDING").limit(limit).stream()
    
    messages = []
    for doc in docs:
        messages.append(doc.to_dict())
    
    return messages[::-1] # Reverse to show oldest at top