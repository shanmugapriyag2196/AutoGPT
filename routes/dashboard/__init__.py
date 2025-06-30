from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__)

from . import business_function_dashboard, dashboard, faiss_store, run_autogpt, response


