import os
from io import BytesIO
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, send_file
from cryptography.fernet import Fernet

encryption_bp = Blueprint('encryption', __name__)

@encryption_bp.route('/encryption')
def home():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template('encryption.html', name=session['user'])

@encryption_bp.route('/encrypt_logic', methods=['POST'])
def encrypt_logic():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    file = request.files.get('file')
    if not file or file.filename == '':
        flash("No file selected.", "danger")
        return redirect(url_for('encryption.home'))

    # Generate key and encrypt
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_data = cipher_suite.encrypt(file.read())

    enc_filename = f"enc_{file.filename}"

    # Prepare file for download
    response = send_file(
        BytesIO(encrypted_data),
        download_name=enc_filename,
        as_attachment=True
    )

    # We send the key in a header, but also flash it for the user
    key_str = key.decode()
    response.headers["X-Encryption-Key"] = key_str
    flash(f"FILE ENCRYPTED! You MUST save this key to decrypt it later: {key_str}", "success")

    return response

@encryption_bp.route('/decrypt_logic', methods=['POST'])
def decrypt_logic():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    file = request.files.get('file')
    key = request.form.get('key')

    if not file or not key:
        flash("Missing file or decryption key.", "danger")
        return redirect(url_for('encryption.home'))

    try:
        cipher_suite = Fernet(key.encode())
        decrypted_content = cipher_suite.decrypt(file.read())

        # Clean up filename (remove 'enc_' prefix if it exists)
        original_name = file.filename.replace('enc_', '')
        
        return send_file(
            BytesIO(decrypted_content),
            download_name=f"decrypted_{original_name}",
            as_attachment=True
        )
    except Exception:
        flash("DECRYPTION FAILED: Invalid Key or Corrupted File.", "danger")
        return redirect(url_for('encryption.home'))