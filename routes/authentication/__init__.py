from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

from . import index, add_record, forgot_password, reset_password, verify_otp, add_recoveryemail, roles_permission  # etc.

