from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from models import init_sqlite_db1
from . import prompt_bp

@prompt_bp.route('/edit_autogpt/<int:prompt_id>', methods=['GET', 'POST'])
def edit_autogpt(prompt_id):
    functions = ['Sales', 'HR', 'Development', 'Resourcing', 'Operations', 'Marketing']
    with sqlite3.connect('autogpt1.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        try:
            cur.execute("ALTER TABLE autogpt1 ADD COLUMN help_text TEXT")
        except sqlite3.OperationalError as e:
            if "duplicate column name" not in str(e):
                raise
            
        if request.method == 'POST':
            name = request.form['gpt_name']
            description = request.form['description']
            businessfunction = request.form['business_function']
            prompt = request.form['prompt']
            template_file = request.form['template_file']
            input_expected = request.form['input_expected']
            version = request.form['version']
            help_text = request.form['help_text']
            cur.execute("""
                UPDATE autogpt1
                SET gpt_name = ?, description = ?, business_function = ?, prompt = ?, template_file = ?, input_expected = ?, version = ?, help_text = ?
                WHERE id = ?
            """, (name, description, businessfunction, prompt, template_file, input_expected, version, help_text, prompt_id))
            conn.commit()
            flash("AutoGPT prompt updated successfully!", "success")
            #return redirect(url_for('view_autogptPermission'))
        cur.execute("SELECT * FROM autogpt1 WHERE id = ?", (prompt_id,))
        prompt = cur.fetchone()
    return render_template('prompt/edit_autogpt.html', prompt=prompt, functions=functions)