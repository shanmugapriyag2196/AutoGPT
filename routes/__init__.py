from .authentication import auth_bp
from .dashboard import dashboard_bp
from .prompt import prompt_bp
from .user.init import user_bp

def register_blueprints(app):
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(prompt_bp)
    app.register_blueprint(user_bp)
