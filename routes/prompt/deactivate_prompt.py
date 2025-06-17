from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from models import init_sqlite_db1
from . import prompt_bp

@prompt_bp.route('/deactivate_prompt/<int:prompt_id>', methods=['POST'])
def deactivate_prompt(prompt_id):
    with sqlite3.connect('autogpt1.db') as conn:
        cur = conn.cursor()
        cur.execute("UPDATE autogpt1 SET status = 'Inactive' WHERE id = ?", (prompt_id,))
        conn.commit()
    flash("Prompt deactivated successfully!", "danger")
    return redirect(url_for('prompt.view_autogptPermission'))