import logging
from flask import Blueprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

lashing_material_bp = Blueprint("lashing_material", __name__, url_prefix="/lashing-material")

@lashing_material_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    response.headers.add('Access-Control-Max-Age', '3600')
    return response

# Import routes to register them with the blueprint
from . import (
                add_lashing_material, get_all_lashing_material, get_lashing_material, 
                update_lashing_material, options, delete_lashing_material, get_lashing_material_from_cargo
            )