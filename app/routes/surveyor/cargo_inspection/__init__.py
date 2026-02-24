import logging
from flask import Blueprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

cargo_inspection_bp = Blueprint("cargo_inspection", __name__, url_prefix="/cargo/inspection")

@cargo_inspection_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT, DELETE')
    response.headers.add('Access-Control-Max-Age', '3600')
    return response

# Import routes to register them with the blueprint
from . import add_cargo_inspection, get_cargo_inspection, update_cargo_inspection, options, delete_cargo_inspection