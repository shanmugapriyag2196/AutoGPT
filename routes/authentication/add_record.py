from flask import Flask, render_template, request, redirect, url_for, flash, session, Blueprint
import sqlite3
from itsdangerous import URLSafeTimedSerializer
#from flask_mail import Mail, Message, mail
from models import init_sqlite_db4
from . import auth_bp

from flask_mail import Message
from flask import current_app
from app import mail

serializer = URLSafeTimedSerializer(auth_bp.secret_key)

# Database connection function
def get_db_connection():
    return sqlite3.connect('user4.db', check_same_thread=False)

@auth_bp.route('/add_record', methods=['GET', 'POST'])
def add_record():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        role = request.form.get('role')
        status = "Active"
        rolebase_gptname = "Select a Role & GPT"

        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO user4 (username, password, email, role, status, rolebase_gptname) VALUES (?, ?, ?, ?, ?, ?)",
                    (username, "", email, role, status, rolebase_gptname)
                )
                conn.commit()

                # Generate password reset link
                token = serializer.dumps(email, salt="password-reset-salt")
                reset_url = url_for('reset_password', token=token, _external=True)

                # Send Welcome Email with Password Setup Link
                try:
                    msg = Message(
                        subject="Welcome to AutoGPT App - Set Your Password",
                        sender=auth_bp.config['MAIL_USERNAME'],
                        recipients=[email],
                        html=f"""
                        <html>
                            <body>
                                <h3>Hi {username},</h3>
                                <p>Thank you for creating an AutoGPT account with us!</p>
                                <p>To set your password, please click the link below:</p>
                                <p><a href="{reset_url}">Create Your Password</a></p>
                                <p>Welcome to the community!</p>
                            </body>
                        </html>
                        """     
                    )
                    mail.send(msg)
                    flash("Please go to your email and Set the password.", 'success')
                except Exception as email_error:
                    flash(f'Failed to send email: {str(email_error)}', 'danger')

        except sqlite3.IntegrityError:
            flash("Error: Email already exists!", 'danger')
        except Exception as db_error:
            flash(f"Error in registration: {str(db_error)}", 'danger')

        return redirect(url_for("add_record"))

    return render_template('add_record.html')