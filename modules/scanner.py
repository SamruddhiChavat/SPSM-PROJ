import requests
import os
from flask import Blueprint, request, flash, redirect, url_for, session, render_template
from database import get_db

scan_bp = Blueprint('scan', __name__)
VT_KEY = os.getenv("VT_API_KEY")

@scan_bp.route('/scanner', methods=['GET', 'POST'])
def scanner():
    if 'user' not in session: return redirect(url_for('auth.login'))
    
    if request.method == 'POST':
        file = request.files.get('file')
        res = requests.post("https://www.virustotal.com/api/v3/files", 
                            files={"file": (file.filename, file.read())}, 
                            headers={"x-apikey": VT_KEY})
        if res.status_code == 200:
            return redirect(url_for('scan.check_result', aid=res.json()['data']['id']))
    return render_template('scanner.html')

@scan_bp.route('/check/<aid>')
def check_result(aid):
    res = requests.get(f"https://www.virustotal.com/api/v3/analyses/{aid}", headers={"x-apikey": VT_KEY})
    data = res.json()
    if data['data']['attributes']['status'] == "completed":
        # Save to DB and show results
        result = "Malicious" if data['data']['attributes']['stats']['malicious'] > 0 else "Safe"
        db = get_db()
        db.execute("INSERT INTO scan_history (username, filename, result) VALUES (?, ?, ?)", 
                   (session['user'], f"Scan_{aid[:5]}", result))
        db.commit()
        flash(f"Scan Result: {result}")
    return redirect(url_for('scan.scanner'))