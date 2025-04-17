from flask import Blueprint

prompt_bp = Blueprint('prompt', __name__)

from . import activate_prompt, deactivate_prompt, edit_autogpt, create_autogpt, view_autogptPermission
