import logging
from flask import Blueprint

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

survey_pdf_bp = Blueprint("survey_pdf", __name__, url_prefix="/survey_pdf")

@survey_pdf_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, OPTIONS, PUT')
    response.headers.add('Access-Control-Max-Age', '3600')
    return response

# Import routes to register them with the blueprint
from . import add_survey_pdf, get_survey_pdf, update_survey_pdf, options, send_survey_pdf