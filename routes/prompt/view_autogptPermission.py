from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from models import init_sqlite_db1
from . import prompt_bp

@prompt_bp.route('/view_autogptPermission', methods=['GET'])
def view_autogptPermission():
    query = request.args.get('query', '').strip()  # Ensure correct variable name

    with sqlite3.connect('autogpt1.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

        if query:
            cur.execute("""
                SELECT id, gpt_name, business_function, timestamp, status
                FROM autogpt1
                WHERE gpt_name LIKE ? OR business_function LIKE ? 
            """, (f'%{query}%', f'%{query}%'))
        else:
            cur.execute("SELECT id, gpt_name, business_function, timestamp, status FROM autogpt1")

        prompts = cur.fetchall()

    return render_template('view_autogptPermission.html', prompts=prompts, query=query)