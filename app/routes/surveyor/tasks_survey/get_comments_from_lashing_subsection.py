from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import tasks_survey_bp, logger
from .schema import comment_list_schema

@tasks_survey_bp.route('/boarding/comments/lashing/<int:id_lashing>/subsection/<int:sub_section_index>', methods=['GET'])
def get_comments_from_lashing_section(id_lashing, sub_section_index):
    """Get comments for a specific lashing"""
    current_session = Session()
    
    try:
        # Check if task exists
        task = current_session.execute(
            text("SELECT id_lashing_material FROM tbl_lashing_material WHERE id_lashing_material = :id"),
            {"id": id_lashing}
        )
        
        if not list(task):
            return jsonify({"error": "Lashing not found"}), 404
            
        # Get all comments for the lashing
        comments = current_session.execute(
            text("""
                SELECT * FROM tbl_comment_survey_boarding
                WHERE id_lashing_material = :id_lashing and sub_section_index = :sub_section_index 
                ORDER BY sub_section_index
            """),
            {
                "id_lashing": id_lashing,
                "sub_section_index": sub_section_index
            }
        )
        
        return comment_list_schema.dumps(comments), 200
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving comments: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()