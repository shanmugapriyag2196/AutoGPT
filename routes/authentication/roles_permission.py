from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from models import init_sqlite_db4
from . import auth_bp

@auth_bp.route('/roles_permission')
#@role_required(['Admin' , 'Manager'])  # Only Admins can access this route
def roles_permission():
    try:
        # Connect to the database and fetch user data
        with sqlite3.connect('user4.db') as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT id, username, email, role FROM user4")
            users = cur.fetchall()
    except Exception as e:
        users = [] 
    # Pass the user's role and users to the template
    user_role = session.get('role', None)  # Get role from session
    return render_template('roles_permission.html')