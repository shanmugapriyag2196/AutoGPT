from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from models import init_sqlite_db1
from . import dashboard_bp

@dashboard_bp.route('/dashboard')
def dashboard():
    try:
        with sqlite3.connect('autogpt1.db') as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            # Predefined business functions
            predefined_functions = ['Sales', 'HR', 'Development', 'Resourcing', 'Operations', 'Marketing']

            # Fetch business functions from the database
            cur.execute("SELECT DISTINCT business_function FROM autogpt1")
            db_functions = [row["business_function"] for row in cur.fetchall()]

            # Combine predefined functions with database functions (avoid duplicates)
            all_business_functions = list(set(predefined_functions + db_functions))

            # Define role-based access to business functions
            role_permissions = {
                'Admin': all_business_functions,
                'Manager': all_business_functions,
                'HR': ['HR'],
                'Developer': ['Development'],
                'Resourcing': ['Resourcing'],
                'Operations': ['Operations'],
                'Marketing': ['Marketing'],
            }

            # Get the user's role from session
            user_role = session.get('role', 'Guest')  # Default to Guest if not set

            # Filter business functions based on the user's role
            business_functions = role_permissions.get(user_role, [])

            # Default icon mapping for business functions
            icon_map = {
                'Sales': 'fas fa-chart-line',
                'HR': 'fas fa-user-friends',
                'Development': 'fas fa-code',
                'Resourcing': 'fas fa-users-cog',
                'Operations': 'fas fa-cogs',
                'Marketing': 'fas fa-bullhorn',
            }

            # Assign icons dynamically with a default icon
            function_icons = {func: icon_map.get(func, 'fas fa-briefcase') for func in business_functions}

    except Exception as e:
        business_functions = []
        function_icons = {}

    return render_template('dashboard.html', business_functions=business_functions, function_icons=function_icons)