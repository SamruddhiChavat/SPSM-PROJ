import jwt
from datetime import datetime, timedelta, timezone
from config import SECRET_KEY

def generate_token(username: str) -> str:
    """Generates a JWT valid for 1 hour."""
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(hours=1), # Expiration time
        "iat": datetime.now(timezone.utc),                      # Issued at time
        "sub": username                                         # Subject (User)
    }
    # Encode using the secret key from config.py and HMAC SHA-256
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def verify_token(token: str):
    """Verifies the JWT and returns the username if valid."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return {"valid": True, "user": payload["sub"]}
    except jwt.ExpiredSignatureError:
        return {"valid": False, "error": "Token has expired. Please log in again."}
    except jwt.InvalidTokenError:
        return {"valid": False, "error": "Invalid token signature."}