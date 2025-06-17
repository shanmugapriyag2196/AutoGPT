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
        cur.execute(
            """
            SELECT id, business_function, gpt_name, version, timestamp, role
            FROM autogpt1
            WHERE business_function = ? AND status = 'Active'
        """, (business_function, ))
        prompts = cur.fetchall()

    # Fetch only ACTIVE users from user4.db matching business_function
    user_data = []
    with sqlite3.connect('user4.db') as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute(
            "SELECT username, rolebase_gptname FROM user4 WHERE status = 'Active'"
        )
        users = cur.fetchall()
    merged_data = []
    for prompt in prompts:
        for user in users:
            entries = user["rolebase_gptname"].split(',')
            for entry in entries:
                parts = entry.strip().split('|')
                if len(parts) == 2 and parts[0] == business_function and parts[
                        1] == prompt["gpt_name"]:
                    merged_data.append({
                        "id": prompt["id"],
                        "version": prompt["version"],
                        "timestamp": prompt["timestamp"],
                        "username": user["username"],
                        "description": parts[1]  # e.g. "Standard Template"
                    })

    return render_template('dashboard/business_function_dashboard.html',
                           function=business_function,
                           query=query,
                           prompts=merged_data)
