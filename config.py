import os

# JWT Secret Key - In production, set this in your environment variables!
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret-security-assignment-key")

# Path to your Firebase credentials file
FIREBASE_CREDENTIALS_PATH = "firebase_credentials.json"