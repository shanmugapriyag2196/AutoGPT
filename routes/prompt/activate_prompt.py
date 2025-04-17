from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from models import init_sqlite_db1
from . import prompt_bp

@prompt_bp.route('/activate_prompt/<int:prompt_id>', methods=['POST'])
def activate_prompt(prompt_id):
    with sqlite3.connect('autogpt1.db') as conn:
        cur = conn.cursor()
        cur.execute("UPDATE autogpt1 SET status = 'Active' WHERE id = ?", (prompt_id,))
        conn.commit()
    flash("Prompt activated successfully!", "success")
    return redirect(url_for('view_autogptPermission'))

