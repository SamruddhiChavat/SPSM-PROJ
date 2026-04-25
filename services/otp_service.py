import pyotp
import qrcode
from io import BytesIO

def generate_totp_secret() -> str:
    """Generates a random base32 secret for Google Authenticator."""
    return pyotp.random_base32()

def get_qr_code(secret: str, username: str) -> bytes:
    """Generates a QR code image buffer for the user to scan."""
    totp = pyotp.TOTP(secret)
    # The provisioning URI sets up the label in the Google Auth app
    uri = totp.provisioning_uri(name=username, issuer_name="SecureSocialApp")
    
    qr = qrcode.make(uri)
    buf = BytesIO()
    qr.save(buf, format="PNG")
    return buf.getvalue()

def verify_totp(secret: str, code: str) -> bool:
    """Verifies the 6-digit code provided by the user."""
    totp = pyotp.TOTP(secret)
    return totp.verify(code)