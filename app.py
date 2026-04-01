import os
from flask import Flask, render_template, session, redirect, url_for
from database import init_db
from modules.auth import auth_bp
from modules.scanner import scan_bp

app = Flask(__name__)

# ✅ USE OLD STYLE (NO ENV CONFUSION)
app.secret_key = "secure_key_guard_portal_2026"

# Initialize DB
init_db()

# Register Blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(scan_bp)


@app.route("/")
def success():
    if 'user' not in session:
        return redirect(url_for('auth.login'))
    return render_template("success.html", name=session['user'])


if __name__ == "__main__":
    app.run(debug=True)