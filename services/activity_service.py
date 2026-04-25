#checks activity log 
from utils.firebase_init import get_db
from datetime import datetime, timezone

def log_activity(username: str, action: str, ip_address: str = "127.0.0.1"):
    """
    Records an auditable event in the database.
    In a real app, ip_address would be pulled from the request headers.
    """
    db = get_db()
    db.collection("activity_logs").add({
        "username": username,
        "action": action,
        "ip": ip_address,
        "timestamp": datetime.now(timezone.utc)
    })