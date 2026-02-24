from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import survey_pdf_bp, logger
from .schema import survey_pdf_list_schema

@survey_pdf_bp.route('/<int:id_demanda>', methods=['GET'])
def get_survey_pdf(id_demanda):
    """Get checklist info for a specific survey"""
    current_session = Session()
    
    try:
        checklist = current_session.execute(
            text("SELECT * FROM tbl_status_pdf WHERE id_demanda = :id_demanda"),
            {"id_demanda": id_demanda}
        )
        
        return survey_pdf_list_schema.dumps(checklist)
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving status PDF: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()