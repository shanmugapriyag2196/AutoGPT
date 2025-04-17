from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from models import init_sqlite_db1
from . import dashboard_bp

@dashboard_bp.route('/run_autogpt/<int:prompt_id>', methods=['GET'])
def run_autogpt(prompt_id):
    with sqlite3.connect('autogpt1.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM autogpt1 WHERE id = ?", (prompt_id,))
        prompt_data = cur.fetchone()

    if not prompt_data:
        return "Prompt not found", 404

    return render_template('run_autogpt.html', prompt_data=prompt_data)