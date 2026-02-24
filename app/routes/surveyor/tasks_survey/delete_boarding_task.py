from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import tasks_survey_bp

@tasks_survey_bp.route('/boarding/<int:task_id>', methods=['DELETE'])
def delete_boarding_task(task_id):
    """Delete a boarding task by id"""
    current_session = Session()
    
    try:
        # Check if task exists
        task = current_session.execute(
            text("SELECT id_task FROM tbl_task_survey_boarding WHERE id_task = :id"),
            {"id": task_id}
        )
        
        if not list(task):
            return jsonify({"error": "Boarding task not found"}), 404
        
        # Delete the task
        current_session.execute(
            text("DELETE FROM tbl_task_survey_boarding WHERE id_task = :id"),
            {"id": task_id}
        )
        
        current_session.commit()
        
        return jsonify({"message": "Boarding task deleted successfully"}), 200
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
