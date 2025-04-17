from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from flask_mail import Mail, Message, mail
from models import init_sqlite_db6, init_sqlite_db4
from . import auth_bp

@auth_bp.route('/add_recoveryemail', methods=['GET', 'POST'])
def add_recoveryemail():
    if request.method == 'POST':
        recovery_email = request.form.get('recoveryemail')
        username = request.form.get('username')
        try:
            with sqlite3.connect('user2.db') as conn:
                cur = conn.cursor()
                cur.execute(
                    "INSERT INTO user2 (username ,recoveryemail) VALUES (?, ?)",
                    (username,recovery_email)  # Ensure all NOT NULL columns are filled
                )
                conn.commit()
            try:
                msg = Message(
                    subject="Welcome to AutoGPT App",
                    sender=auth_bp.config['MAIL_USERNAME'],
                    recipients=[recovery_email],
                    html=f"""
                    <html>
                        <body>
                            <h3>Hi {username},</h3>
                            <p>Your recovery email has been successfully updated in our system.</p>
                            <p>If this wasn't you, please contact support immediately.</p>
                        </body>
                    </html>
                    """     
                )
                mail.send(msg)
                flash('Add Recovery Email successful!', 'success')
            except Exception as email_error:
                flash(f'Failed to send email: {str(email_error)}', 'danger')
        except Exception as db_error:
            flash(f"Error in registration: {str(db_error)}", 'danger')
        return redirect(url_for("add_recoveryemail"))
    with sqlite3.connect('user4.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT email, password FROM user4 WHERE email = ?", (session['email'],))
        user = cur.fetchone()
    if not user:
        session.clear()
        return redirect(url_for('dashboard'))
    # Pass the user data to the template
    return render_template('add_recoveryemail.html', user={
        'email': user[0],
        'password': user[1]
    })