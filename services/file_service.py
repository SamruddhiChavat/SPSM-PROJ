
import requests
import time
import streamlit as st

# Replace with your actual key from VirusTotal
VT_API_KEY = "abeff87ab76d18e12e40a45b36acd93c0c55f9081db91809b86911afeb29a4a7"

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 Megabytes

def validate_file(file_name: str, file_size: int) -> tuple:
    """Basic bouncer check for size and extension."""
    if '.' not in file_name:
        return False, "File has no extension."
    ext = file_name.rsplit('.', 1)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        return False, f"Invalid type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
    if file_size > MAX_FILE_SIZE:
        return False, "File exceeds 5MB limit."
    return True, "Valid"

def scan_with_virustotal(file_bytes: bytes) -> tuple:
    """
    Real-time VirusTotal Scanning.
    Returns (is_clean: bool, message: str)
    """
    if not VT_API_KEY or "YOUR_PASTE" in VT_API_KEY:
        return False, "VirusTotal API Key not configured in file_service.py"

    headers = {"x-apikey": VT_API_KEY}
    
    try:
        # 1. Upload file to VirusTotal
        files = {"file": ("upload_file", file_bytes)}
        response = requests.post("https://www.virustotal.com/api/v3/files", headers=headers, files=files)
        
        if response.status_code != 200:
            return False, f"VT Upload Failed: {response.json().get('error', {}).get('message', 'Unknown error')}"

        analysis_id = response.json()["data"]["id"]
        
        # 2. Poll for results 
        # Free API tier is slow; we wait and check
        with st.spinner("Analyzing with 70+ Antivirus engines..."):
            for _ in range(5):  # Try 5 times (total 50 seconds wait)
                time.sleep(10)
                report_url = f"https://www.virustotal.com/api/v3/analyses/{analysis_id}"
                report_resp = requests.get(report_url, headers=headers)
                
                if report_resp.status_code == 200:
                    attributes = report_resp.json()["data"]["attributes"]
                    status = attributes["status"]
                    
                    if status == "completed":
                        stats = attributes["stats"]
                        malicious = stats.get("malicious", 0)
                        suspicious = stats.get("suspicious", 0)
                        
                        if malicious > 0 or suspicious > 0:
                            return False, f"Malicious content detected! (Flagged by {malicious} engines)"
                        return True, "File is clean."
        
        return False, "Scanning timed out. Please try again."

    except Exception as e:
        return False, f"Security Service Error: {str(e)}"