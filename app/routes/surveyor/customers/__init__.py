import logging
from flask import Blueprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

customers_bp = Blueprint("customers", __name__, url_prefix="/customers")

@customers_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
    response.headers.add('Access-Control-Max-Age', '3600')
    return response

# Import routes to register them with the blueprint
from . import add_customer, get_all_customers, get_customer_by_id, search_customer, options