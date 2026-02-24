import logging
from flask import Blueprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

lifting_material_bp = Blueprint("lifting_material", __name__, url_prefix="/lifting-material")

@lifting_material_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    response.headers.add('Access-Control-Max-Age', '3600')
    return response

# Import routes to register them with the blueprint
from . import (
                add_lifting_material, get_all_lifting_material, get_lifting_material, 
                update_lifting_material, options, delete_lifting_material, get_lifting_material_from_cargo
            )