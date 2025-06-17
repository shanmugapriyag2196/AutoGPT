from flask import Blueprint

user_bp = Blueprint('user', __name__)

from . import activate_user, deactivate_user, edit_user, my_profile, view_usersPermission
