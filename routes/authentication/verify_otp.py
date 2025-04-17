from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from flask_mail import Mail, Message, mail
import time
from models import init_sqlite_db4
from . import auth_bp

@auth_bp.route('/verify_otp', methods=['GET', 'POST'])
def verify_otp():
    entered_otp = request.form.get('otp')
    otp = session.get('otp')
    otp_expiry_time = session.get('otp_expiry')
    # Step 3: Check if the OTP exists and has not expired
    if not otp or not otp_expiry_time:
        flash("OTP has expired or is not valid.", "danger")
        return redirect(url_for('forgot_password'))
    if time.time() > otp_expiry_time:
        flash("OTP has expired.", "danger")
        return redirect(url_for('forgot_password'))
    # Step 4: Validate OTP
    if entered_otp == otp:
        # OTP is correct, allow the user to reset the password
        new_password = request.form.get('new_password')
        email = session.get('user_email')
        try:
            # Update the user's password in the database
            with sqlite3.connect('user4.db') as conn:
                cur = conn.cursor()
                cur.execute("UPDATE user4 SET password = ? WHERE email = ?", (new_password, email))
                conn.commit()
                if cur.rowcount > 0:
                    flash("Password updated successfully! Please log in.", "success")
                else:
                    flash("No user found with the provided username.", "danger")
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")
        # After resetting password, clear OTP data from session
        session.pop('otp', None)
        session.pop('otp_expiry', None)
        session.pop('user_email', None)
        return redirect(url_for('index'))
    else:
        flash("Invalid OTP. Please try again.", "danger")
        return redirect(url_for('verify_otp'))