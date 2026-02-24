from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import tasks_survey_bp, logger
from .schema import comment_list_schema

@tasks_survey_bp.route('/boarding/comments/<int:comment_id>', methods=['GET'])
def get_comment_by_id(comment_id):
    """Get a specific comment by ID"""
    current_session = Session()
    
    try:
        # Get comment data
        comment = current_session.execute(
            text("SELECT * FROM tbl_comment_survey_boarding WHERE id_comment = :id"),
            {"id": comment_id}
        )
        
        comment_data = comment_list_schema.dump(comment)
        
        if not comment_data:
            return jsonify({"error": "Comment not found"}), 404
            
        return jsonify(comment_data[0])
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving comment: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()