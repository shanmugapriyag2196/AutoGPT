from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from models import init_sqlite_db4
from . import user_bp

#app = Flask(__name__)

@user_bp.route('/activate_user/<int:user_id>', methods=['POST'])
def activate_user(user_id):
    with sqlite3.connect('user4.db') as conn:
        cur = conn.cursor()
        cur.execute("UPDATE user4 SET status = 'Active' WHERE id = ?", (user_id,))
        conn.commit()
    flash("User activated successfully!", "success")
    return redirect(url_for('user.view_usersPermission'))
