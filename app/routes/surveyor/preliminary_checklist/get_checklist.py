from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import checklist_bp, logger
from .schema import checklist_list_schema

@checklist_bp.route('/<int:id_survey>', methods=['GET'])
def get_checklist(id_survey):
    """Get checklist info for a specific survey"""
    current_session = Session()
    
    try:
        checklist = current_session.execute(
            text("SELECT * FROM tbl_preliminary_checklist WHERE id_survey = :id_survey"),
            {"id_survey": id_survey}
        )
        
        return checklist_list_schema.dumps(checklist)
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving preliminary checklist: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()