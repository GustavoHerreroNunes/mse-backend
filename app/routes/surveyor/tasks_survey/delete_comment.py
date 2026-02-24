from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import tasks_survey_bp

@tasks_survey_bp.route('/boarding/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    """Delete a comment by id"""
    current_session = Session()
    
    try:
        # Check if comment exists
        comment = current_session.execute(
            text("SELECT id_comment FROM tbl_comment_survey_boarding WHERE id_comment = :id"),
            {"id": comment_id}
        )
        
        if not list(comment):
            return jsonify({"error": "Comment not found"}), 404
        
        # Delete the comment
        current_session.execute(
            text("DELETE FROM tbl_comment_survey_boarding WHERE id_comment = :id"),
            {"id": comment_id}
        )
        
        current_session.commit()
        
        return jsonify({"message": "Comment deleted successfully"}), 200
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
