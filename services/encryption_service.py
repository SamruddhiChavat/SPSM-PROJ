#file encrypt decrypt service
from cryptography.fernet import Fernet
import os

# --- MASTER KEY (Keep this if you use it for string/chat messages) ---
KEY_FILE = "aes_secret.key"
if not os.path.exists(KEY_FILE):
    with open(KEY_FILE, "wb") as key_file:
        key_file.write(Fernet.generate_key())
        
with open(KEY_FILE, "rb") as key_file:
    MASTER_KEY = key_file.read()
    
master_cipher = Fernet(MASTER_KEY)

def encrypt_message(message: str) -> str:
    return master_cipher.encrypt(message.encode('utf-8')).decode('utf-8')

def decrypt_message(encrypted_message: str) -> str:
    try:
        return master_cipher.decrypt(encrypted_message.encode('utf-8')).decode('utf-8')
    except Exception:
        return "[Decryption Failed]"


# --- NEW: PER-FILE ZERO-KNOWLEDGE ENCRYPTION ---
def generate_file_key() -> bytes:
    """Generates a brand new, unique AES key for a specific file."""
    return Fernet.generate_key()

def encrypt_file_data(file_bytes: bytes, key: bytes) -> bytes:
    """Encrypts file bytes using the uniquely provided key."""
    f = Fernet(key)
    return f.encrypt(file_bytes)

def decrypt_file_data(encrypted_bytes: bytes, key: bytes) -> bytes:
    """Decrypts file bytes using the uniquely provided key."""
    f = Fernet(key)
    try:
        return f.decrypt(encrypted_bytes)
    except Exception as e:
        raise ValueError("Decryption failed. Incorrect key or corrupted file.") from e