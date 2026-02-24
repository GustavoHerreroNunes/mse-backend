from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import tasks_survey_bp, logger
from .schema import comment_list_schema

@tasks_survey_bp.route('/boarding/comments/task/<int:task_id>/section/<int:section_index>', methods=['GET'])
def get_comments_from_task_section(task_id, section_index):
    """Get comments for a specific task"""
    current_session = Session()
    
    try:
        # Check if task exists
        task = current_session.execute(
            text("SELECT id_task FROM tbl_task_survey_boarding WHERE id_task = :id"),
            {"id": task_id}
        )
        
        if not list(task):
            return jsonify({"error": "Task not found"}), 404
            
        # Get all photos for the task
        photos = current_session.execute(
            text("""
                    SELECT * FROM tbl_comment_survey_boarding
                    WHERE id_task = :task_id 
                    AND section_index = :section_index 
                    ORDER BY section_index;
            """),
            {
                "task_id": task_id,
                "section_index": section_index
            }
        )
        
        return comment_list_schema.dumps(photos), 200
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving comments: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()