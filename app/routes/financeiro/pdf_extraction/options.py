from flask import Blueprint
from . import pdf_extraction_bp

@pdf_extraction_bp.route('/extract', methods=['OPTIONS'])
def options():
    """Handle OPTIONS requests for CORS preflight"""
    return '', 200