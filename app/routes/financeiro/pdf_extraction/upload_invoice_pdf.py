from flask import request, jsonify, current_app
from sqlalchemy import text
import logging
import json
import os
from werkzeug.utils import secure_filename

from app.services import Session
from . import pdf_extraction_bp
from app.utils.upload_pdf_to_drive import upload_invoice_to_drive

logger = logging.getLogger(__name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@pdf_extraction_bp.route('/upload', methods=['POST'])
def upload_invoice_pdf():
    """
    Upload PDF invoice file to Google Drive.
    
    Expects multipart/form-data with:
    - file: PDF file
    - data: JSON with id_demanda field
    
    Returns upload confirmation with Google Drive URL.
    """
    current_session = Session()
    
    try:
        # Validate request has file part
        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "message": "No file part in the request",
                "url": None
            }), 400
        
        file = request.files['file']
        
        # Validate file was selected
        if file.filename == '':
            return jsonify({
                "success": False,
                "message": "No file selected",
                "url": None
            }), 400
        
        # Validate file extension
        if not file or not allowed_file(file.filename):
            return jsonify({
                "success": False,
                "message": "Invalid file type. Only PDF files are allowed",
                "url": None
            }), 400
        
        # Get and validate JSON data
        if 'data' not in request.form:
            return jsonify({
                "success": False,
                "message": "Missing 'data' field with id_demanda information",
                "url": None
            }), 400
        
        try:
            json_data = json.loads(request.form['data'])
        except json.JSONDecodeError:
            return jsonify({
                "success": False,
                "message": "Invalid JSON format in 'data' field",
                "url": None
            }), 400
        
        # Validate required fields
        id_demanda = json_data.get('id_demanda')
        if not id_demanda:
            return jsonify({
                "success": False,
                "message": "Missing 'id_demanda' field",
                "url": None
            }), 400
        
        # Check if demanda exists and get Google Drive folder ID
        demanda_result = current_session.execute(
            text("SELECT id_pasta_gd_demanda FROM tbl_demandas WHERE id_demanda = :id_demanda"),
            {"id_demanda": id_demanda}
        ).fetchone()
        
        if not demanda_result:
            return jsonify({
                "success": False,
                "message": f"Demanda with id {id_demanda} not found",
                "url": None
            }), 404
        
        id_pasta_gd_demanda = demanda_result[0]
        if not id_pasta_gd_demanda:
            return jsonify({
                "success": False,
                "message": "Missing Google Drive Folder ID for this demanda",
                "url": None
            }), 400
        
        # Save file temporarily
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'uploads'), filename)
        
        # Ensure upload directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)
        
        try:
            # Upload to Google Drive
            uploaded_url = upload_invoice_to_drive(file_path, id_pasta_gd_demanda)
            
            if not uploaded_url:
                return jsonify({
                    "success": False,
                    "message": "Failed to upload to Google Drive",
                    "url": None
                }), 500
            
            logger.info(f"Successfully uploaded invoice PDF for demanda {id_demanda} to Google Drive")
            
            return jsonify({
                "success": True,
                "message": "Invoice PDF uploaded successfully to Google Drive",
                "url": uploaded_url,
                "id_demanda": id_demanda
            }), 200
            
        finally:
            # Clean up temporary file
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"Temporary file {file_path} cleaned up")
            except Exception as cleanup_error:
                logger.warning(f"Failed to clean up temporary file {file_path}: {cleanup_error}")
    
    except Exception as e:
        logger.error(f"Unexpected error in upload_invoice_pdf: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Internal server error",
            "url": None
        }), 500
    
    finally:
        current_session.close()

@pdf_extraction_bp.route('/upload', methods=['OPTIONS'])
def upload_invoice_pdf_options():
    """Handle OPTIONS request for CORS"""
    return '', 200