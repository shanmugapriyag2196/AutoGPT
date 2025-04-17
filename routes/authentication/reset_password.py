from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
import re
from get_next_version import is_strong_password
from itsdangerous import URLSafeTimedSerializer
from models import init_sqlite_db4
from . import auth_bp

serializer = URLSafeTimedSerializer(auth_bp.secret_key)

# Database connection function
def get_db_connection():
    return sqlite3.connect('user4.db', check_same_thread=False)

@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt="password-reset-salt", max_age=86400)  # 24 hours expiration
    except:
        flash("The password reset link is invalid or has expired.", "danger")
        return redirect(url_for("add_record"))

    if request.method == 'POST':
        new_password = request.form.get('password')

        # Validate strong password
        if not is_strong_password(new_password):
            flash("Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, a number, and a special character.", "danger")
            return redirect(url_for("reset_password", token=token))

        # Store the password in the same format as entered
        stored_password = new_password  # No hashing, stores the exact input

        with get_db_connection() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE user4 SET password = ? WHERE email = ?", (stored_password, email))
            conn.commit()

        flash("Your password has been set successfully. You can now log in!", "success")
        return redirect(url_for("index"))  # Redirect to login page

    return render_template('reset_password.html', token=token)