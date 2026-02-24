import logging
from flask import Blueprint

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

attendants_survey_bp = Blueprint('attendants-survey', __name__, url_prefix="/attendants-survey")

# CORS config
@attendants_survey_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
    response.headers.add('Access-Control-Max-Age', '3600')
    return response

# Importa as rotas e associa ao blueprint
from . import create_attendant, get_attendants_by_task, delete_attendant, options