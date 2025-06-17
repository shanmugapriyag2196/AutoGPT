from flask import Flask
from config import Config
from extension import db, mail, migrate
from models import init_sqlite_db1, init_sqlite_db4, init_sqlite_db6, MeetingResponse
from dotenv import load_dotenv
from routes import register_blueprints
import os

load_dotenv()  # Load environment variables from .env

#openai_api_key=os.getenv("OPENAI_API_KEY")  # Use this if needed

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    with app.app_context():
        init_sqlite_db1()
        init_sqlite_db4()
        init_sqlite_db6()
        db.create_all()

    register_blueprints(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)