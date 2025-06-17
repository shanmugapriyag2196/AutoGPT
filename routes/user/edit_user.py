from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from functools import wraps
from models import init_sqlite_db4, init_sqlite_db1
from . import user_bp

def role_required(allowed_roles):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if 'role' not in session or session['role'] not in allowed_roles:
                flash("You do not have permission to access this page.", "danger")
                return redirect(url_for('dashboard'))
            return func(*args, **kwargs)
        return wrapper
    return decorator

@user_bp.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
@role_required(['Admin', 'Manager', 'Developer', 'HR']) 
def edit_user(user_id):
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        role = request.form['role']
        #rolebase_gptname = request.form['rolebase_gptname'] 
        rolebase_gptname_list = request.form.getlist('rolebase_gptname')
        rolebase_gptname = ','.join(rolebase_gptname_list)

        with sqlite3.connect('user4.db') as conn:
            cur = conn.cursor()
            cur.execute(
                "UPDATE user4 SET username = ?, email = ?, role = ?, rolebase_gptname = ? WHERE id = ?",
                (username, email, role, rolebase_gptname, user_id))
            conn.commit()

        flash("User updated successfully!", "success")
        return redirect(url_for('user.view_usersPermission'))

    # ✅ Fetch user details from user4.db
    with sqlite3.connect('user4.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM user4 WHERE id = ?", (user_id, ))
        user = cur.fetchone()

    # ✅ Fetch all Role & GPT Name pairs from autogpt.db (for all users)
    with sqlite3.connect('autogpt1.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT business_function, gpt_name FROM autogpt1"
                    )  # Fetching all roles & GPT names
        business_functions = [(row['business_function'], row['gpt_name'])
                              for row in cur.fetchall()]

    return render_template('user/edit_user.html',
                           user=user,
                           business_functions=business_functions)