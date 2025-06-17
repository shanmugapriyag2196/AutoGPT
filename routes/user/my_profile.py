from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3, os
from models import init_sqlite_db4
from . import user_bp

@user_bp.route('/my_profile', methods=['GET', 'POST'])
def my_profile():
    # Ensure the user is logged in
    if 'email' not in session:
        flash("You need to log in to access this page.", "danger")
        return redirect(url_for('auth.index'))
    # Get the logged-in user's email from the session
    email = session['email']
    if request.method == 'POST':
        # Update the user's profile information
        new_username = request.form['username']
        new_email = request.form['email']
        new_role = request.form['role']
        new_password = request.form['password']
        try:
            # Update user details in the database
            with sqlite3.connect('user4.db') as conn:
                cur = conn.cursor()
                cur.execute("""
                    UPDATE user4
                    SET username = ?, email = ?, role = ?, password = ?
                    WHERE email = ?
                """, (new_username, new_email, new_role, new_password, email))
                conn.commit()
                # Update the session email if it has changed
                session['email'] = new_email
                flash("Profile updated successfully", "success")
        except Exception as e:
            flash(f"Error updating profile: {str(e)}", "danger")
    # Fetch the updated user details from the database
    with sqlite3.connect('user4.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT username, email, role, password FROM user4 WHERE email = ?", (session['email'],))
        user = cur.fetchone()
    if not user:
        session.clear()
        return redirect(url_for('auth.index'))
    # Pass the user data to the template
    return render_template('user/my_profile.html', user={
        'username': user[0],
        'email': user[1],
        'role': user[2],
        'password': user[3]
    })