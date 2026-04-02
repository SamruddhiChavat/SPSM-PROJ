import os
from flask import Flask, render_template, session, redirect, url_for
from database import init_db, get_db
from modules.auth import auth_bp
from modules.scanner import scan_bp

app = Flask(__name__)

# Secret key
app.secret_key = "secure_key_guard_portal_2026"

# Initialize DB
init_db()

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(scan_bp)

# ---------------- DASHBOARD ----------------
@app.route("/")
def dashboard():
    if 'user' not in session:
        return redirect(url_for('auth.login'))

    user = session['user']
    db = get_db()

    # Total scans
    total = db.execute(
        "SELECT COUNT(*) FROM scan_history WHERE username = ?",
        (user,)
    ).fetchone()[0]

    # Safe scans
    safe = db.execute(
        "SELECT COUNT(*) FROM scan_history WHERE username = ? AND result = 'Safe'",
        (user,)
    ).fetchone()[0]

    # Score calculation
    score = int((safe / total * 100)) if total > 0 else 100

    # Recent activity
    history = db.execute(
        "SELECT filename, result FROM scan_history WHERE username = ? ORDER BY timestamp DESC LIMIT 3",
        (user,)
    ).fetchall()

    return render_template(
        "success.html",
        name=user,
        score=score,
        total=total,
        activity=history
    )


# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)