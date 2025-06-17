from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint, current_app
import sqlite3
#from flask_mail import Mail, Message, mail
import time
import datetime
from datetime import date
import random
from . import auth_bp
from flask_mail import Message
from extension import mail

@auth_bp.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form.get('username')
        new_password = request.form.get('new_password')
        email = request.form.get('email') 
        # Validate inputs
        if not email or not new_password:
            flash("Username and new password cannot be empty.", "danger")
            return redirect(url_for('auth.forgot_password'))
        # Step 1: Generate and store OTP in session
        otp = str(random.randint(100000, 999999))  # Generate a 6-digit OTP
        otp_expiry_time = time.time() + 300  # OTP expires in 5 minutes
        session['otp'] = otp
        session['otp_expiry'] = otp_expiry_time
        session['user_email'] = email
        # Step 2: Send the OTP via email
        try:
            msg = Message(
                subject="Your OTP for Password Reset",
                sender=current_app.config['MAIL_USERNAME'],
                recipients=[email],
                html=f"""
                <html>
                    <body>
                        <h3>Hello {username},</h3>
                        <p>Your OTP to reset the password is: <strong>{otp}</strong></p>
                        <p>This OTP will expire in 5 minutes.</p>
                    </body>
                </html>
                """
            )
            mail.send(msg)
            flash('An OTP has been sent to your email address.', 'info')
        except Exception as email_error:
            flash(f'Failed to send email: {str(email_error)}', 'danger')
        return render_template('authentication/verify_otp.html')  # Render OTP input page
    return render_template('authentication/forgot_password.html')