from flask import jsonify
from sqlalchemy import text
from app.services import Session
from . import attendants_survey_bp
from .schema import attendant_survey_list_schema

@attendants_survey_bp.route('/task/<int:task_id>', methods=['GET'])
def get_attendants_by_task(task_id):
    """Get all attendants for a specific task"""
    current_session = Session()
    try:
        task_check = current_session.execute(
            text("SELECT id_task FROM tbl_task_survey WHERE id_task = :id"),
            {"id": task_id}
        )
        if not list(task_check):
            return jsonify({"error": "Task not found"}), 404

        attendants = current_session.execute(
            text("SELECT * FROM tbl_attendant_survey_boarding WHERE id_task = :id_task ORDER BY id_attendant"),
            {"id_task": task_id}
        )
        return attendant_survey_list_schema.dumps(attendants), 200
    except Exception as e:
        current_session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()
