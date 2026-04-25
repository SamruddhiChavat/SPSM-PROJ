import bcrypt
from utils.firebase_init import get_db

def hash_password(password: str) -> str:
    """Hashes a plaintext password using bcrypt."""
    # gensalt() generates a secure, randomized salt automatically
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifies a plaintext password against the stored bcrypt hash."""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_user(username: str, password_hash: str, totp_secret: str):
    """Saves a new user to the Firestore database."""
    db = get_db()
    db.collection("users").document(username).set({
        "password": password_hash,
        "totp_secret": totp_secret,
        "role": "user"
    })

def get_user(username: str):
    """Retrieves a user document from Firestore."""
    db = get_db()
    doc = db.collection("users").document(username).get()
    if doc.exists:
        return doc.to_dict()
    return None