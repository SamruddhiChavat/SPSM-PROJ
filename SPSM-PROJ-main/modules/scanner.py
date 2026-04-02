import requests
import os
import time
from dotenv import load_dotenv
from flask import Blueprint, request, flash, redirect, url_for, session, render_template
from database import get_db

# Load environment variables
load_dotenv()

scan_bp = Blueprint('scan', __name__)

VT_KEY = os.getenv("VT_API_KEY")

# ---------------- SCANNER ----------------
@scan_bp.route('/scanner', methods=['GET', 'POST'])
def scanner():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        file = request.files.get('file')

        # Safety check
        if not file or file.filename == "":
            flash("No file selected.", "danger")
            return redirect(url_for('scan.scanner'))

        try:
            res = requests.post(
                "https://www.virustotal.com/api/v3/files",
                files={"file": (file.filename, file.read())},
                headers={"x-apikey": VT_KEY}
            )

            if res.status_code == 200:
                analysis_id = res.json()['data']['id']
                flash("File uploaded. Checking results...", "info")
                return redirect(url_for('scan.check_result', aid=analysis_id))
            else:
                print(res.text)
                flash("VirusTotal API error.", "danger")

        except Exception as e:
            print(e)
            flash("Something went wrong during scanning.", "danger")

    return render_template('scanner.html')


# ---------------- CHECK RESULT (AUTO RETRY) ----------------
@scan_bp.route('/check/<aid>')
def check_result(aid):
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    try:
        # Try multiple times
        for _ in range(5):  # 5 attempts
            res = requests.get(
                f"https://www.virustotal.com/api/v3/analyses/{aid}",
                headers={"x-apikey": VT_KEY}
            )

            data = res.json()
            status = data['data']['attributes']['status']

            if status == "completed":
                malicious = data['data']['attributes']['stats']['malicious']
                result = "Malicious" if malicious > 0 else "Safe"

                # Save to DB
                db = get_db()
                db.execute(
                    "INSERT INTO scan_history (username, filename, result) VALUES (?, ?, ?)",
                    (session['user'], f"Scan_{aid[:5]}", result)
                )
                db.commit()

                flash(
                    f"Scan Result: {result}",
                    "success" if result == "Safe" else "danger"
                )

                return redirect(url_for('scan.scanner'))

            # Wait before retry
            time.sleep(3)

        # If still not ready
        flash("Scan taking longer than expected. Try again.", "warning")

    except Exception as e:
        print(e)
        flash("Error fetching scan result.", "danger")

    return redirect(url_for('scan.scanner'))