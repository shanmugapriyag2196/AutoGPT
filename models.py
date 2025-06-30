from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3, os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from extension import db

app = Flask(__name__)  
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///responses.db'  # Use SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class MeetingResponse(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_input = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

def init_sqlite_db4():         
    with sqlite3.connect('user4.db') as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS user4(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL,
            role TEXT NOT NULL,
            status TEXT NOT NULL,
            rolebase_gptname TEXT NOT NULL
        )
        """)
    conn.close()
init_sqlite_db4()

def init_sqlite_db6():           # Database setup function   
    with sqlite3.connect('user2.db') as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS user2(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            recoveryemail TEXT NOT NULL
        )
        """)
    conn.close()
init_sqlite_db6()

def init_sqlite_db1():
    with sqlite3.connect('autogpt1.db') as conn:
        conn.execute("""
        CREATE TABLE IF NOT EXISTS autogpt1 (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            business_function TEXT NOT NULL,
            gpt_name TEXT NOT NULL,
            description TEXT NOT NULL,
            prompt TEXT NOT NULL,
            template_file TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            username TEXT NOT NULL,        
            role TEXT NOT NULL,
            version TEXT NOT NULL,
            input_expected TEXT NOT NULL,
            status,
            help_text
        )
        """)
    conn.close()
init_sqlite_db1()

with app.app_context():     # Initialize database
    db.create_all()



import os
from libsql_client import create_client_sync

def get_conn_autogpt1():
    return create_client_sync(url=os.getenv("TURSO_URL_autogpt1"), auth_token=os.getenv("TURSO_TOKEN_autogpt1"))

def get_conn_user2():
    return create_client_sync(url=os.getenv("TURSO_URL_user2"), auth_token=os.getenv("TURSO_TOKEN_user2"))

def get_conn_user4():
    return create_client_sync(url=os.getenv("TURSO_URL_user4"), auth_token=os.getenv("TURSO_TOKEN_user4"))
