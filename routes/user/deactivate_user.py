from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from models import init_sqlite_db4
from . import user_bp

@user_bp.route('/deactivate_user/<int:user_id>', methods=['POST'])
def deactivate_user(user_id):
    with sqlite3.connect('user4.db') as conn:
        cur = conn.cursor()
        cur.execute("UPDATE user4 SET status = 'Inactive' WHERE id = ?", (user_id,))
        conn.commit()
    flash("User deactivated successfully!", "danger")
    return redirect(url_for('user.view_usersPermission'))