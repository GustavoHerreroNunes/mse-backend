import logging
from flask import Blueprint

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

pdf_extraction_bp = Blueprint('pdf_extraction', __name__, url_prefix="/pdf_extraction")

# CORS config
@pdf_extraction_bp.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
    response.headers.add('Access-Control-Max-Age', '3600')
    return response

# Import routes and associate with blueprint
from . import extract_invoice_data, upload_invoice_pdf, options