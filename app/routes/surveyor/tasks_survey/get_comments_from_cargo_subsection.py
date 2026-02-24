from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import tasks_survey_bp, logger
from .schema import comment_list_schema

@tasks_survey_bp.route('/boarding/comments/cargo/<int:id_cargo>/subsection/<int:sub_section_index>', methods=['GET'])
def get_comments_from_cargo_section(id_cargo, sub_section_index):
    """Get comments for a specific cargo"""
    current_session = Session()
    
    try:
        # Check if task exists
        task = current_session.execute(
            text("SELECT cargo_id FROM tbl_cargo WHERE cargo_id = :id"),
            {"id": id_cargo}
        )
        
        if not list(task):
            return jsonify({"error": "Cargo not found"}), 404
            
        # Get all comments for the cargo
        comments = current_session.execute(
            text("""
                SELECT * FROM tbl_comment_survey_boarding
                WHERE id_cargo = :id_cargo and sub_section_index = :sub_section_index 
                ORDER BY sub_section_index
            """),
            {
                "id_cargo": id_cargo,
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