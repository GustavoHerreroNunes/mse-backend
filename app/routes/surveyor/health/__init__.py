import logging
from flask import Blueprint

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

health_bp = Blueprint('health', __name__, url_prefix="/health")

# CORS config
@health_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
    response.headers.add('Access-Control-Max-Age', '3600')
    return response

# Importa as rotas e associa ao blueprint
from . import health_check, options