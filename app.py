from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_migrate import Migrate
from models import init_sqlite_db1, init_sqlite_db4, init_sqlite_db6
from dotenv import load_dotenv
from routes import register_blueprints

db = SQLAlchemy()
mail = Mail()
migrate = Migrate()

load_dotenv()  # Load environment from .env

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    # Initialize SQLite
    with app.app_context():
        init_sqlite_db1()
        init_sqlite_db4()
        init_sqlite_db6()
        db.create_all()

    # Register Blueprints
    register_blueprints(app)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
