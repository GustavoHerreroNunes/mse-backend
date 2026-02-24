import logging
from flask import Blueprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

lifting_inspection_bp = Blueprint("lifting_inspection", __name__, url_prefix="/lifting/inspection")

@lifting_inspection_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    response.headers.add('Access-Control-Max-Age', '3600')
    return response

# Import routes to register them with the blueprint
from . import add_lifting_inspection, get_lifting_inspection, update_lifting_inspection, options, delete_lifting_inspection