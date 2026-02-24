from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import tasks_survey_bp
from .schema import task_survey_list_schema

@tasks_survey_bp.route('/boarding/<int:task_id>', methods=['GET'])
def get_boarding_task_by_id(task_id):
    """Get boarding task data by id"""
    current_session = Session()
    
    try:
        task = current_session.execute(
            text("SELECT * FROM tbl_task_survey_boarding WHERE id_task = :id"),
            {"id": task_id}
        )
        
        task_data = task_survey_list_schema.dump(task)
        
        if not task_data:
            return jsonify({"error": "Boarding task not found"}), 404
            
        return jsonify(task_data[0])
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()