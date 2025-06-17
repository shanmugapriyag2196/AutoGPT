from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from models import init_sqlite_db1
from . import dashboard_bp
from flask import jsonify

@dashboard_bp.route('/run_autogpt/<int:prompt_id>', methods=['GET'])
def run_autogpt(prompt_id):
    with sqlite3.connect('autogpt1.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM autogpt1 WHERE id = ?", (prompt_id,))
        prompt_data = cur.fetchone()

    if not prompt_data:
        return "Prompt not found", 404

    return render_template('dashboard/run_autogpt.html', prompt_data=prompt_data)


@dashboard_bp.route('/get-help-text/<int:prompt_id>')
def get_help_text(prompt_id):
    try:
        with sqlite3.connect('autogpt1.db') as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute("SELECT help_text FROM autogpt1 WHERE id = ?", (prompt_id,))
            row = cur.fetchone()
            return jsonify({"help_text": row["help_text"] if row else "Help text not found."})
    except Exception as e:
        return jsonify({"help_text": f"Error: {str(e)}"}), 500
    return render_template('dashboard/run_autogpt.html', prompt_data=prompt_data)


