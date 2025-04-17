from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from models import init_sqlite_db1, init_sqlite_db4
from . import dashboard_bp

@dashboard_bp.route('/dashboard/<business_function>')
def business_function_dashboard(business_function):
    query = request.args.get('query', '').strip()

    # Fetch prompts from autogpt1.db
    with sqlite3.connect('autogpt1.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("""
            SELECT id, business_function, gpt_name, version, timestamp, role
            FROM autogpt1
            WHERE business_function = ? AND status = 'Active'
        """, (business_function,))
        prompts = cur.fetchall()

    # Fetch only ACTIVE users from user4.db matching business_function
    user_data = []
    with sqlite3.connect('user4.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT username, rolebase_gptname FROM user4 WHERE status = 'Active'")
        users = cur.fetchall()

        for row in users:
            rolebase_parts = row["rolebase_gptname"].split('|')
            if rolebase_parts and rolebase_parts[0] == business_function:
                user_data.append({
                    "username": row["username"],
                    "description": rolebase_parts[-1]
                })

    return render_template(
        'business_function_dashboard.html',
        function=business_function,
        query=query,
        prompts=prompts,
        users=user_data
    )