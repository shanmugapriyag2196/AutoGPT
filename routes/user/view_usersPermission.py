from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3, os
from functools import wraps
from models import init_sqlite_db4
from . import user_bp

def role_required(allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] not in allowed_roles:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for('dashboard.dashboard'))
            return func(*args, **kwargs)
        return wrapper
    return decorator

@user_bp.route('/view_usersPermission', methods=['GET'])
@role_required(['Admin'])  # Only Admins can access this route
def view_usersPermission():
    query = request.args.get('query', '').strip()  # Get the search query from the request
    try:
        # Connect to the database and fetch user data
        with sqlite3.connect('user4.db') as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            # Check if a search query is provided
            if query:
                # Filter users based on the search query (matching username or email)
                cur.execute("""
                    SELECT id, username, email, role, rolebase_gptname 
                    FROM user4 
                    WHERE username LIKE ? OR email LIKE ? OR role LIKE ? OR status LIKE ? OR rolebase_gptname LIKE ?
                    
                """, (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'))
            else:
                # Fetch all users if no search query
                cur.execute("SELECT id, username, email, role, status, rolebase_gptname FROM user4")
            
            users = cur.fetchall()
            
    except Exception as e:
        users = []
    return render_template('user/view_usersPermission.html', users=users, query=query)