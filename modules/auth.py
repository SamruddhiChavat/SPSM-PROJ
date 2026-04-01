import pyotp
import qrcode
import base64
from io import BytesIO
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from database import get_db, generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__)

# ---------------- SIGNUP ----------------
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user = request.form.get("username")
        pw = request.form.get("password")

        if not user or not pw:
            flash("All fields required", "danger")
            return redirect(url_for('auth.signup'))

        mfa_secret = pyotp.random_base32()
        hashed_pw = generate_password_hash(pw)

        try:
            db = get_db()
            db.execute(
                "INSERT INTO users (username, password, mfa_secret) VALUES (?, ?, ?)",
                (user, hashed_pw, mfa_secret)
            )
            db.commit()

            # Generate QR
            qr_uri = pyotp.TOTP(mfa_secret).provisioning_uri(
                name=user, issuer_name="GuardPortal"
            )

            buf = BytesIO()
            qrcode.make(qr_uri).save(buf, format="PNG")

            return render_template(
                "verify_mfa.html",
                qr_image=base64.b64encode(buf.getvalue()).decode(),
                first_time=True
            )

        except Exception as e:
            print(e)
            flash("Username already exists.", "danger")

    return render_template("signup.html")


# ---------------- LOGIN ----------------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = request.form.get("username")
        pw = request.form.get("password")

        db_user = get_db().execute(
            "SELECT * FROM users WHERE username = ?",
            (user,)
        ).fetchone()

        if db_user and check_password_hash(db_user['password'], pw):
            session['temp_user'] = user
            return render_template("verify_mfa.html", first_time=False)

        flash("Invalid credentials.", "danger")

    return render_template("login.html")


# ---------------- VERIFY MFA ----------------
@auth_bp.route("/verify_mfa", methods=["POST"])
def verify_mfa():
    user = session.get('temp_user')

    if not user:
        return redirect(url_for('auth.login'))

    otp = request.form.get("otp_code")

    db_user = get_db().execute(
        "SELECT mfa_secret FROM users WHERE username = ?",
        (user,)
    ).fetchone()

    if db_user and pyotp.TOTP(db_user['mfa_secret']).verify(otp):
        session['user'] = user
        session.pop('temp_user', None)
        return redirect(url_for('success'))   # IMPORTANT FIX

    flash("Wrong MFA.", "danger")
    return redirect(url_for('auth.login'))


# ---------------- LOGOUT ----------------
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('auth.login'))