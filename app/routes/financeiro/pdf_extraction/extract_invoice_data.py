from flask import request, jsonify
import logging
from werkzeug.utils import secure_filename
from . import pdf_extraction_bp
from .schema import (
    pdf_extraction_request_schema, 
    nf_extraction_result_schema,
    nd_extraction_result_schema, 
    invoice_extraction_result_schema,
    extraction_response_schema
)
from .pdf_processor import InvoiceDataExtractor

logger = logging.getLogger(__name__)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@pdf_extraction_bp.route('/extract', methods=['POST'])
def extract_invoice_data():
    """
    Extract data from PDF invoice files.
    
    Expects multipart/form-data with:
    - file: PDF file
    - data: JSON with tipo_nota field
    
    Returns extracted invoice data or error message.
    """
    try:
        # Validate request has file part
        if 'file' not in request.files:
            return jsonify({
                "success": False,
                "message": "No file part in the request",
                "extracted_data": None
            }), 400
        
        file = request.files['file']
        
        # Validate file was selected
        if file.filename == '':
            return jsonify({
                "success": False,
                "message": "No file selected",
                "extracted_data": None
            }), 400
        
        # Validate file extension
        if not file or not allowed_file(file.filename):
            return jsonify({
                "success": False,
                "message": "Invalid file type. Only PDF files are allowed",
                "extracted_data": None
            }), 400
        
        # Get and validate JSON data
        if 'data' not in request.form:
            return jsonify({
                "success": False,
                "message": "Missing 'data' field with tipo_nota information",
                "extracted_data": None
            }), 400
        
        try:
            import json
            json_data = json.loads(request.form['data'])
        except json.JSONDecodeError:
            return jsonify({
                "success": False,
                "message": "Invalid JSON format in 'data' field",
                "extracted_data": None
            }), 400
        
        # Validate JSON schema
        try:
            validated_data = pdf_extraction_request_schema.load(json_data)
        except Exception as e:
            return jsonify({
                "success": False,
                "message": f"Validation error: {str(e)}",
                "extracted_data": None
            }), 400
        
        tipo_nota = validated_data['tipo_nota']
        
        # Read PDF content
        try:
            pdf_content = file.read()
        except Exception as e:
            logger.error(f"Error reading PDF file: {str(e)}")
            return jsonify({
                "success": False,
                "message": "Error reading PDF file",
                "extracted_data": None
            }), 500
        
        # Initialize extractor and validate PDF
        extractor = InvoiceDataExtractor()
        
        # Validate PDF content
        if not extractor.pdf_processor.validate_pdf_content(pdf_content):
            return jsonify({
                "success": False,
                "message": "Invalid PDF file or PDF without extractable text",
                "extracted_data": None
            }), 400
        
        # Extract data from PDF
        try:
            extracted_data = extractor.extract_data(pdf_content, tipo_nota)

            # Serialize extracted data using appropriate schema
            if tipo_nota == "NF-e":
                serialized_data = nf_extraction_result_schema.dump(extracted_data)
            elif tipo_nota == "ND":
                serialized_data = nd_extraction_result_schema.dump(extracted_data)
            elif tipo_nota == "Invoice":
                serialized_data = invoice_extraction_result_schema.dump(extracted_data)
            
            return jsonify({
                "success": True,
                "message": "Data extracted successfully",
                "extracted_data": serialized_data
            }), 200
            
        except Exception as e:
            logger.error(f"Error extracting data from PDF: {str(e)}")
            return jsonify({
                "success": False,
                "message": f"Error extracting data from PDF: {str(e)}",
                "extracted_data": None
            }), 500
    
    except Exception as e:
        logger.error(f"Unexpected error in extract_invoice_data: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Internal server error",
            "extracted_data": None
        }), 500