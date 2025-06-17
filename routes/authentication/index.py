from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3, os
from . import auth_bp

@auth_bp.route('/', methods=['GET', 'POST'])
@auth_bp.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
       
        with sqlite3.connect('user4.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM user4 WHERE email = ? AND password = ?", (email, password))
            user = cur.fetchone()
        if user:
            session['email'] = user[3]
            session['role'] = user[4]
            return redirect(url_for('dashboard.dashboard'))
        else:
            flash("Invalid email or password.", "danger")
    return render_template('authentication/index.html')
