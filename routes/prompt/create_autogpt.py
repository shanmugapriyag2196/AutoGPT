from flask import Flask, render_template, request, redirect, url_for, flash, session, current_app
import sqlite3
import os
import time
import datetime
from datetime import date
from datetime import datetime
from config import Config
from models import init_sqlite_db1, init_sqlite_db4
from . import prompt_bp

@prompt_bp.route('/create_autogpt', methods=['GET', 'POST'])
def create_autogpt():
    functions = ['Sales', 'HR', 'Development', 'Resourcing', 'Operations', 'Marketing']
    
    # Ensure user is logged in
    if 'email' not in session:
        flash("Please log in to continue.", "danger")
        return redirect(url_for('auth.index'))  # Redirect to index if not logged in

    email = session['email']  # Get logged-in user's email

    # Fetch username and role of the logged-in user
    with sqlite3.connect('user4.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT username, role FROM user4 WHERE email = ?", (email,))
        user1 = cur.fetchone()

    if not user1:
        session.clear()
        flash("User not found. Please log in again.", "danger")
        return redirect(url_for('auth.index'))  # Ensure user is logged in

    username, role = user1  # Extract user details

    if request.method == 'POST':    
        # Get form data
        business_function = request.form.get('business_function')
        gpt_name = request.form.get('gpt_name')
        description = request.form.get('description')
        prompt = request.form.get('prompt')
        template_file = request.files.get('template_file')
        version = request.form.get('version')
        input_expected = request.form.get('input_expected')
        status = "Active"
        help_text = request.form.get('help_text')

        # Save uploaded file and get its path
        template_file_path = None
        if template_file and template_file.filename != '':
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            template_file_path = os.path.join(upload_folder, template_file.filename)
            template_file.save(template_file_path)

        try:
            # Insert data into autogpt1.db with the correct username and role
            with sqlite3.connect('autogpt1.db') as conn:
                cur = conn.cursor()
                try:
                   cur.execute("ALTER TABLE autogpt1 ADD COLUMN help_text TEXT")
                except sqlite3.OperationalError:
                   pass

                cur.execute(''' 
                    INSERT INTO autogpt1
                    (business_function, gpt_name, description, prompt, template_file, timestamp, username, role, version, input_expected, status, help_text) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
                ''', (business_function, gpt_name, description, prompt, template_file_path, datetime.now().strftime('%d-%m-%Y'), username, role, version, input_expected, status, help_text))
                conn.commit()
                flash('AutoGPT created and stored in the database successfully!', 'success')
        except Exception as e:
            flash(f'Error saving AutoGPT: {str(e)}', "danger")

        return render_template('prompt/create_autogpt.html', functions=functions)  # Render the same page with flash message

    return render_template('prompt/create_autogpt.html', functions=functions)