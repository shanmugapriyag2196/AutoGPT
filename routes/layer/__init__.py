from flask import Blueprint

layer_bp = Blueprint('layer', __name__)

from . import hr_layer, marketing_layer, development_layer, operation_layer, resourcing_layer, sales_layer


