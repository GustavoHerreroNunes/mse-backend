from flask import jsonify
from sqlalchemy import text

from app.services import Session
from . import demandas_bp, logger
from ..tasks_survey.schema import task_survey_list_schema

@demandas_bp.route('/<int:id_demanda>/tarefas/surveyor/', methods=['GET'])
def get_all_tasks_from_survey(id_demanda):
    """Get all tasks for a specific survey"""
    current_session = Session()
    
    try:
        tasks = current_session.execute(
            text("SELECT * FROM tbl_task_survey WHERE id_survey = :survey_id ORDER BY id_task"),
            {"survey_id": id_demanda}
        )
        
        return task_survey_list_schema.dumps(tasks)
    except Exception as e:
        current_session.rollback()
        logger.error(f"Error retrieving tasks: {str(e)}")
        return jsonify({"error": str(e)}), 500
    finally:
        current_session.close()