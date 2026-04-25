import smtplib
import random
import string
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- SMTP CONFIGURATION ---
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "samruddhichavat@gmail.com" 

# IMPORTANT: This must be the 16-character Google App Password (no spaces)
SENDER_PASSWORD = "kell anxu dqxw pnnb" 

def send_recovery_email(receiver_email):
    """
    Generates a unique 6-character recovery token and sends it 
    via SMTP to the specified receiver email address.
    """
    # Generate a random 6-character alphanumeric token
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    try:
        # 1. Create the Email Message
        msg = MIMEMultipart()
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email
        msg['Subject'] = "🔐 Secure Recovery Token"

        body = f"""
        Hello,

        Your account recovery token is: {token}

        Please enter this code in the Secure Portal to verify your identity 
        and reset your password. If you did not request this, please secure 
        your account immediately.

        Do not share this code with anyone.
        """
        msg.attach(MIMEText(body, 'plain'))

        # 2. Establish Secure Connection with SMTP Server
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()  # Upgrade the connection to secure TLS
        
        # 3. Authenticate and Send
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)
        server.quit()
        
        # Return True and the token so it can be saved in session_state for verification
        return True, token

    except Exception as e:
        # Return False and the error message to display in the Streamlit UI
        return False, str(e)